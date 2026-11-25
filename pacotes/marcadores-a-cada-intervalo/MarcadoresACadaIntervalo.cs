// Marcadores a cada intervalo: põe um marcador a cada INTERVALO_SEGUNDOS
// dentro da seleção de tempo ou, sem seleção, do início do projeto até o fim
// do último evento. Licença: MIT OR Apache-2.0.

using System;
using ScriptPortal.Vegas;

public class EntryPoint
{
    // Altere aqui o espaço entre os marcadores.
    const double INTERVALO_SEGUNDOS = 5.0;
    const int MAX_MARCADORES = 1000;

    public void FromVegas(Vegas vegas)
    {
        Timecode inicio = vegas.Transport.SelectionStart;
        Timecode fim = inicio + vegas.Transport.SelectionLength;
        if (vegas.Transport.SelectionLength.Milliseconds <= 0)
        {
            inicio = new Timecode();
            fim = new Timecode();
            foreach (Track trilha in vegas.Project.Tracks)
            {
                foreach (TrackEvent ev in trilha.Events)
                {
                    if (ev.End > fim) fim = ev.End;
                }
            }
        }
        Timecode passo = Timecode.FromSeconds(INTERVALO_SEGUNDOS);
        int n = 0;
        for (Timecode t = inicio; t < fim && n < MAX_MARCADORES; t = t + passo)
        {
            n++;
            vegas.Project.Markers.Add(new Marker(t, "Marcador " + n));
        }
    }
}
